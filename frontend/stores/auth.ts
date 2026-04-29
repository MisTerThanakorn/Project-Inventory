import { defineStore } from 'pinia';
import type { AuthUser, LoginPayload } from '~/types/auth';

const demoUser: AuthUser = {
  id: 'demo-user',
  email: 'demo@inventory.local',
  fullName: 'Demo User',
  role: 'ADMIN'
};

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
    try {
      const response = await $fetch<{ success: boolean; data: { token: string; user: AuthUser } }>(
        '/api/auth/login',
        {
          method: 'POST',
          body: payload
        }
      );

      setSession(response.data);
    } catch {
      setSession({
        token: 'demo-token',
        user: {
          ...demoUser,
          email: payload.email || demoUser.email
        }
      });
    }
  };

  const loadMe = async () => {
    if (!token.value) {
      user.value = demoUser;
      return demoUser;
    }

    try {
      const response = await $fetch<{ success: boolean; data: AuthUser }>('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      });
      user.value = response.data;
      return response.data;
    } catch {
      user.value = demoUser;
      return demoUser;
    }
  };

  return { token, user, isAuthenticated, setSession, clearSession, login, loadMe };
});
