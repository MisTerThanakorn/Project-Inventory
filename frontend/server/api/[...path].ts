export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const path = getRequestURL(event).pathname.replace(/^\/api\//, '');
  const url = `${config.public.backendUrl}/api/${path}`;
  const method = event.method;
  const headers = getRequestHeaders(event);
  const forwardHeaders: Record<string, string> = {};

  for (const [key, value] of Object.entries(headers)) {
    if (key !== 'host' && typeof value === 'string') {
      forwardHeaders[key] = value;
    }
  }
  const body = ['GET', 'HEAD'].includes(method) ? undefined : await readBody(event);

  return await $fetch(url, {
    method,
    headers: forwardHeaders,
    body
  });
});
