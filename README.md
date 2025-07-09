# 🌟 InspAIre – Personalized AI-Powered Visual Inspiration

**InspAIre** is an MVP web application that helps users get personalized improvement suggestions based on uploaded images and their preferences. It uses a multi-agent AI pipeline to analyze environments, detect objects, and provide meaningful visual and textual enhancements – from meal planning to interior design.

---

## 🚀 Features

- **User Profile Onboarding**
  - Simple step-by-step form
  - Collects non-sensitive preferences (e.g., food, colors, style, hobbies)

- **Image Upload**
  - Upload or capture 3 high-resolution images
  - Converts iPhone HEIC to JPEG/PNG automatically
  - Compresses to minimize storage size

- **Multi-Agent AI System**
  - **Agent 1**: Detects the type of environment (e.g., kitchen, workshop, living room)
  - **Agent 2**: Performs object detection and categorization
  - **Agent 3**: Generates personalized suggestions and a new improved image using AI

- **Examples**
  - 🧊 Fridge Scan → Meal plan + shopping list + filled fridge image
  - 🛋️ Living Room → Furniture advice + materials list + redesigned room image

---

## 🛠 Tech Stack

| Layer         | Technology                          |
|--------------|-------------------------------------|
| Frontend      | React (TypeScript, Redux Toolkit)   |
| Backend       | Flask + PostgreSQL                  |
| AI Services   | OpenAI / Local Vision Models        |
| File Storage  | Local or S3-compatible              |
| Deployment    | Docker + Compose                    |
| Hosting       | 🇩🇪 GDPR-compliant (e.g. Hetzner)   |

---

## 📦 Monorepo Structure

inspaire/
├── apps/
│ ├── api/ # Flask backend
│ ├── web/ # React frontend
│ └── mobile/ # (Optional future)
├── services/
│ ├── environment-detector/
│ ├── object-detector/
│ └── recommender/
├── libs/ # Shared types & utils
├── infra/ # Docker, nginx, k8s
├── scripts/ # Build/dev scripts
└── docker-compose.yml

---

## 🧑‍💻 Local Development

### Prerequisites
- Docker + Docker Compose
- Node.js + Yarn (for frontend)

### Start the app

```bash
# Start all services
docker-compose up --build
```

---

---

## 🧪 API Endpoints (MVP)

| Method | Endpoint             | Description                        |
|--------|----------------------|------------------------------------|
| POST   | `/api/profile`       | Create user profile                |
| POST   | `/api/upload-images` | Upload 3 images for analysis       |
| GET    | `/api/analysis/:id`  | Get personalized AI suggestion     |

---

## 🤝 Contributing

We welcome contributions! To get started:

1. **Fork** the repository
2. Create a new **feature branch**:  
   `git checkout -b feat/your-feature`
3. **Commit** your changes:  
   `git commit -m "feat: short description"`
4. **Push** to your fork:  
   `git push origin feat/your-feature`
5. **Open a Pull Request** on the `main` branch

### Code Style
- Backend: PEP8 + Flake8
- Frontend: ESLint + Prettier
- Use meaningful commit messages (Conventional Commits recommended)

---

## 📄 License

This project is currently under **development** and released as open source under the **MIT License**.

---

## 🙌 Credits

InspAIre is designed to help users discover the full potential of their environments using the power of personalized, explainable AI. Built with ❤️ by humans, enhanced by agents.