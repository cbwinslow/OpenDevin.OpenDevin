import { setInitialized } from "../state/taskSlice";
import store from "../store";
import ActionType from "../types/ActionType";
import { SupportedSettings } from "../types/ConfigType";
import Socket from "./socket";
import { setByKey } from "../state/settingsSlice";
import toast from "../utils/toast";

export type Settings = { [key: string]: string };

export async function fetchModels() {
  const response = await fetch(`/api/litellm-models`);
  return response.json();
}

export async function fetchAgents() {
  const response = await fetch(`/api/agents`);
  return response.json();
}

// all available settings in the frontend
// TODO: add the values to i18n to support multi languages
const DISPLAY_MAP: { [key: string]: string } = {
  LLM_MODEL: "model",
  AGENT: "agent",
  LANGUAGE: "language",
  LLM_API_KEY: "api key",
  LLM_BASE_URL: "base url",
};

const DEFAULT_SETTINGS: Settings = {
  LLM_MODEL: "gpt-3.5-turbo",
  AGENT: "MonologueAgent",
  LANGUAGE: "en",
  LLM_API_KEY: "",
  LLM_BASE_URL: "https://openrouter.ai/api/v1",
};

const getSettingOrDefault = (key: string): string => {
  const value = localStorage.getItem(key);
  return value || DEFAULT_SETTINGS[key];
};

export const getCurrentSettings = (): Settings => ({
  LLM_MODEL: getSettingOrDefault("LLM_MODEL"),
  AGENT: getSettingOrDefault("AGENT"),
  LANGUAGE: getSettingOrDefault("LANGUAGE"),
  LLM_API_KEY: getSettingOrDefault("LLM_API_KEY"),
  LLM_BASE_URL: getSettingOrDefault("LLM_BASE_URL"),
});

// Function to merge and update settings
export const getUpdatedSettings = (
  newSettings: Settings,
  currentSettings: Settings,
) => {
  const updatedSettings: Settings = {};
  SupportedSettings.forEach((setting) => {
    if (newSettings[setting] !== currentSettings[setting]) {
      updatedSettings[setting] = newSettings[setting];
    }
  });
  return updatedSettings;
};

const dispatchSettings = (updatedSettings: Record<string, string>) => {
  let i = 0;
  for (const [key, value] of Object.entries(updatedSettings)) {
    store.dispatch(setByKey({ key, value }));
    if (key in DISPLAY_MAP) {
      setTimeout(() => {
        toast.settingsChanged(`Set ${DISPLAY_MAP[key]} to "${value}"`);
      }, i * 500);
      i += 1;
    }
  }
};

export const initializeAgent = () => {
  const event = { action: ActionType.INIT, args: getCurrentSettings() };
  const eventString = JSON.stringify(event);
  store.dispatch(setInitialized(false));
  Socket.send(eventString);
};

// Save and send settings to the server
export function saveSettings(newSettings: Settings): void {
  const currentSettings = getCurrentSettings();
  const updatedSettings = getUpdatedSettings(newSettings, currentSettings);

  if (Object.keys(updatedSettings).length === 0) {
    return;
  }

  dispatchSettings(updatedSettings);
  initializeAgent();
}
