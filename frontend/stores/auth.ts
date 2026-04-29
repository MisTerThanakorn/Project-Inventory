import { defineStore } from 'pinia';
import type { AuthUser, LoginPayload } from '~/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const token = useCookie<string | null>('pi_token', { default: () => null, sameSite: 'lax' });
  const user = ref<AuthUser | null>(null);

  const isAuthenticated = computed(() => Boolean(token.value));

  const setSession = (payload: { token: string; user: AuthUser }) => {
    token.value = payload.token;
    user.value = payload.user;
  };

  const clearSession = () => {
    token.value = null;
    user.value = null;
  };

  const login = async (payload: LoginPayload) => {
    const response = await $fetch<{ success: boolean; data: { token: string; user: AuthUser } }>(
      '/api/auth/login',
      {
        method: 'POST',
        body: payload
      }
    );

    setSession(response.data);
  };

  const loadMe = async () => {
    if (!token.value) return null;
    const response = await $fetch<{ success: boolean; data: AuthUser }>('/api/auth/me', {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    });
    user.value = response.data;
    return response.data;
  };

  return { token, user, isAuthenticated, setSession, clearSession, login, loadMe };
});

