<template>
  <div class="auth-wrap">
    <section class="auth-grid">
      <div class="auth-hero card">
        <p class="eyebrow">{{ t('topbar.eyebrow') }}</p>
        <h1>{{ t('login.title') }}</h1>
        <p class="muted">{{ t('login.subtitle') }}</p>

        <div class="auth-points">
          <div class="point">
            <span class="point-dot" />
            Desktop-ready workspace
          </div>
          <div class="point">
            <span class="point-dot" />
            Tablet-friendly controls
          </div>
          <div class="point">
            <span class="point-dot" />
            Mobile-first layout
          </div>
        </div>
      </div>

      <section class="auth card">
        <h2>{{ t('login.title') }}</h2>
        <p class="muted">{{ t('login.subtitle') }}</p>

        <form class="grid" @submit.prevent="onSubmit">
          <label class="field">
            <span>{{ t('login.email') }}</span>
            <InputText v-model="form.email" type="email" autocomplete="email" fluid />
          </label>
          <label class="field">
            <span>{{ t('login.password') }}</span>
            <Password v-model="form.password" :feedback="false" toggle-mask fluid input-class="w-full" />
          </label>

          <Button type="submit" :label="t('login.submit')" icon="pi pi-sign-in" />
        </form>

        <Message v-if="errorMessage" severity="error" :closable="false">{{ errorMessage }}</Message>
      </section>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n();
const auth = useAuthStore();

const form = reactive({
  email: '',
  password: ''
});

const errorMessage = ref('');

const onSubmit = async () => {
  errorMessage.value = '';
  try {
    await auth.login(form);
    await navigateTo('/dashboard');
  } catch (error: any) {
    errorMessage.value = error?.data?.message || error?.message || 'Login failed';
  }
};
</script>

<style scoped>
.auth-wrap {
  min-height: calc(100vh - 2rem);
  display: grid;
  place-items: center;
  padding: 1rem;
}

.auth-grid {
  width: min(1080px, 100%);
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 1rem;
}

.auth-hero,
.auth {
  padding: 1.6rem;
}

.auth-hero {
  display: grid;
  align-content: space-between;
  min-height: 460px;
  background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.16), transparent 26%),
    radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.14), transparent 24%),
    rgba(15, 23, 42, 0.78);
}

.auth-hero h1,
.auth h2 {
  margin: 0.35rem 0 0.6rem;
  font-size: clamp(1.8rem, 3vw, 2.4rem);
}

.auth-points {
  display: grid;
  gap: 0.75rem;
}

.point {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  color: #dbeafe;
}

.point-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--accent);
  box-shadow: 0 0 0 5px rgba(56, 189, 248, 0.12);
}

.auth {
  width: 100%;
  align-self: center;
}

.auth .grid {
  margin-top: 1rem;
}

.auth :deep(.p-message) {
  margin-top: 1rem;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.72rem;
  color: var(--accent);
}

h1 {
  margin-top: 0;
}

@media (max-width: 960px) {
  .auth-grid {
    grid-template-columns: 1fr;
  }

  .auth-hero {
    min-height: auto;
  }
}

@media (max-width: 640px) {
  .auth-wrap {
    padding: 0.5rem;
  }

  .auth-hero,
  .auth {
    padding: 1.2rem;
    border-radius: 20px;
  }
}
</style>
