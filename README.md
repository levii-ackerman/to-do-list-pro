# ✅ To-Do List App (FastAPI asosida)

Bu loyiha FastAPI asosida yaratilgan zamonaviy **To-Do List** ilovasi bo‘lib, foydalanuvchilarga shaxsiy va guruh vazifalarini yaratish, boshqarish va eslatmalar olish imkonini beradi. Loyihada foydalanuvchilar o‘rtasidagi do‘stlik, guruh ishlari, eslatmalar va taglar tizimi mavjud.

!!! hozircha friend qo'shish to'g'ridan to'g'ri amalga oshiriladi. FriendRequest qo'shilmagan
!!! Tag va Notificationlar ham qo'shilmagan.

---

## ✨ Xususiyatlar

- 👤 Foydalanuvchi ro‘yxatdan o‘tishi va tizimga kirishi (Login / Signup)
- ✅ Oddiy (shaxsiy) tasklar yaratish va boshqarish
- 👥 Guruhlar yaratish va guruh a'zolarini qo‘shish
- 📋 Guruh tasklarini yaratish va a’zolarga biriktirish
- 🏷 Tasklarga `#tag` belgilari qo‘shish
- 🔔 Deadline uchun avtomatik eslatmalar yuborish
- 🤝 Foydalanuvchilar o‘rtasida do‘stlik va do‘stlik so‘rovlarini yuborish
- 🕒 (Optional) Tasklar bo‘yicha tarixni saqlash (`TaskLog` modeli)

---

## 🧱 Texnologiyalar

- **Backend**: FastAPI
- **ORM**: SQLAlchemy (async)
- **Ma'lumotlar bazasi**: PostgreSQL (yoki boshqa SQL bazasi)
- **Tokenlar**: JWT autentifikatsiya
- **Eslatmalar**: Foydalanuvchiga push yoki xabar tarzida

---

## 📁 Loyiha tuzilmasi (misol)

├── app/
│ ├── models/ # Pydantic & ORM modellar
│ ├── schemas/ # Pydantic so‘rov va javob sxemalari
│ ├── routes/ # API endpointlari
│ ├── services/ # Biznes mantiq
│ └── utils/ # Foydali funksiyalar (auth, JWT)
├── main.py # Asosiy FastAPI ilovasi
├── requirements.txt # Kutubxonalar ro‘yxati
└── README.md # Hujjat


---

## 🧩 Model ro‘yxati

1. **User** – foydalanuvchi ma’lumotlari (ro‘yxatdan o‘tish, kirish)
2. **Task** – oddiy shaxsiy task
3. **TaskLog** – tasklar tarixini saqlash (opsional)
4. **FriendRequest** – do‘stlik so‘rovlari (pending, accepted)
5. **Group** – foydalanuvchi guruhlari (masalan, jamoa)
6. **GroupMember** – guruhga a’zo bo‘lgan foydalanuvchi
7. **GroupTask** – guruh tasklari
8. **GroupTaskAssignment** – guruh tasklarini a’zolarga biriktirish
9. **Tag** – tasklarga belgilash uchun taglar
10. **Notification** – deadline eslatmalari
11. **Friendship** – do‘stlik munosabati

---

## ⚙️ O‘rnatish

```bash
# Reponi klon qiling:
git clone https://github.com/levii-ackerman/todo-list-fastapi.git
cd todo-list-fastapi

# Virtual muhit yaratish:
pipenv shell
yoki
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Kutubxonalarni o‘rnatish:
pip install -r requirements.txt

# ishga tushirish
uvicorn main:app --reload

# .env fayl namunasi
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60


# savol va takliflar bo'lsa murojaat qiling
