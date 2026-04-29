export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const path = getRequestURL(event).pathname.replace(/^\/api\//, '');
  const url = `${config.public.backendUrl}/api/${path}`;
  const method = event.method;
  const headers = getRequestHeaders(event);
  delete headers.host;
  const body = ['GET', 'HEAD'].includes(method) ? undefined : await readBody(event);

  return await $fetch(url, {
    method,
    headers,
    body
  });
});
