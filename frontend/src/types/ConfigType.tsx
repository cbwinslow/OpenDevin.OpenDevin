enum ArgConfigType {
  LLM_MODEL = "LLM_MODEL",
  AGENT = "AGENT",
  LANGUAGE = "LANGUAGE",
  LLM_API_KEY = "LLM_API_KEY",
  LLM_BASE_URL = "LLM_BASE_URL",
}

const SupportedSettings: string[] = [
  ArgConfigType.LLM_MODEL,
  ArgConfigType.AGENT,
  ArgConfigType.LANGUAGE,
  ArgConfigType.LLM_API_KEY,
  ArgConfigType.LLM_BASE_URL,
];

export { ArgConfigType, SupportedSettings };
