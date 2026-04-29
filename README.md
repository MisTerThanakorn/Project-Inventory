# Project Inventory

Monorepo สำหรับระบบ Inventory Management แบบแยก Frontend และ Backend ตามแผนใน `inventory-plan.md`.

## โครงสร้าง

- `backend/` - Node.js API, Prisma, PostgreSQL
- `frontend/` - Nuxt 3, Vue 3, Pinia, i18n

## เริ่มต้น

1. ติดตั้ง dependencies
2. ตั้งค่าไฟล์ `.env` ของ backend และ frontend
3. รันฐานข้อมูล Prisma migrate
4. สั่ง `npm run dev`

## Backend

API หลัก:

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/items`
- `POST /api/items`
- `GET /api/items/:id`
- `PATCH /api/items/:id`
- `DELETE /api/items/:id`
- `GET /api/dashboard/summary`

Backend ตอนนี้ใช้ Python + FastAPI + SQLAlchemy ตามที่ขอ

## ติดตั้งฝั่ง Python

```bash
cd backend
pip install -r requirements.txt
```

## Frontend

- หน้า login
- dashboard
- รายการสินค้า
- ฟอร์มเพิ่ม/แก้ไขสินค้า
- รองรับภาษาไทย/อังกฤษ
