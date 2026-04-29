export interface AuthUser {
  id: string;
  email: string;
  fullName: string;
  role: 'ADMIN' | 'STAFF';
}

export interface LoginPayload {
  email: string;
  password: string;
}

