export default defineNuxtRouteMiddleware(() => {
  const token = useCookie<string | null>('pi_token');

  if (!token.value) {
    return navigateTo('/login');
  }
});

