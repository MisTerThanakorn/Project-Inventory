# แผนการสร้างระบบสต๊อกสินค้า (Inventory Management System) แบบแยกส่วน (Frontend & Backend)
ด้วย Nuxt 3, Node.js และ i18n

เอกสารฉบับนี้ออกแบบมาเพื่อให้คุณสามารถใช้เป็น "Master Plan" และใช้ "Prompts" เพื่อสั่งงาน AI ให้เขียนโค้ดได้อย่างมีระเบียบและเป็นระบบ

---

## 1. โครงสร้างโครงการ (Project Architecture)

เราจะแยกส่วนกันโดยใช้แนวทาง Monorepo หรือแยกโฟลเดอร์ให้ชัดเจน:

```text
inventory-project/
├── backend/                # Node.js (Express/Fastify) + Prisma + PostgreSQL
│   ├── src/
│   │   ├── controllers/    # ควบคุม Logic ของ API
│   │   ├── routes/         # เส้นทาง API
│   │   ├── middlewares/    # การตรวจสอบสิทธิ์ (Auth)
│   │   └── services/       # การติดต่อ Database
│   ├── prisma/             # Database Schema
│   └── .env                # ค่ากำหนดความลับต่างๆ
│
├── frontend/               # Nuxt 3 (Vue 3)
│   ├── components/         # UI Components แยกตามส่วนงาน
│   ├── lang/               # i18n (th.json, en.json)
│   ├── pages/              # ระบบ Routing อัตโนมัติ
│   ├── server/             # API Proxy/BFF
│   ├── stores/             # Pinia (State Management)
│   ├── types/              # TypeScript Interfaces
│   └── nuxt.config.ts      # การตั้งค่า Nuxt และ i18n