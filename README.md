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
```text
inspaire/
├── apps/
│ ├── api/ # Flask backend
│ ├── web/ # React frontend
│ └── mobile/ # (Optional future)
├── services/
│ ├── image-processing/
│ ├── environment-detector/
│ ├── object-detector/
│ └── recommender/
├── libs/ # Shared types & utils
├── infra/ # Docker, nginx, k8s
├── scripts/ # Build/dev scripts
└── docker-compose.yml
```

---

## 🧑‍💻 Local Development

### Prerequisites
- Docker + Docker Compose
- Node.js + Yarn (for frontend)

### Start the app

```bash
# Start all services
docker-compose up --build

# database migrations
docker-compose exec backend flask db migrate -m "Add db tables"
docker-compose exec backend flask db upgrade

```

---

### Make API calls
__pofile__: 
 * url = http://127.0.0.1:5000/api/profile
 * method = POST
 * header = Content-Type: application/json
 * body = 
 ```json 
    {
      "favorite_food": "Italienisch",
      "hobbies": "Gartenarbeit, Kochen",
      "job": "Handwerker",
      "color_preferences": "[\"grün\", \"braun\"]",
      "material_preferences": "Holz, Rustikal",
      "abo_state": "premium"
    }
```
__image upload__: 
 * url = http://localhost:5000/api/upload-images
 * method = POST
 * header = Content-Type: multipart/form-data; boundary=<calculated when request is sent>
 * body = 
   * Key = user_id, Value = 1
   * Key = images, Value = select your image 1
   * Key = images, Value = select your image 2
   * Key = images, Value = select your image 3

__analyze environment__: 
 * url = http://localhost:5000/api/analyze-environment
 * method = POST
 * header = Content-Type: application/json
 * body = 
 ```json 
    {
      "user_id": 1
    }
```
__analyze objects__: 
 * url = http://localhost:5000/api/analyze-objects
 * method = POST
 * header = Content-Type: application/json
 * body = 
 ```json 
    {
      "user_id": 1
    }
```

__generate prompt for recommendation__: 
 * url = http://localhost:5000/api/generate-prompt
 * method = POST
 * header = Content-Type: application/json
 * body = 
 ```json 
    {
      "user_id": 1
    }
```

__generate response for recommendation__: 
 * url = http://localhost:5000/api/generate-response
 * method = POST
 * header = Content-Type: application/json
 * body = 
 ```json 
    {
      "user_id": 1
    }
```
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

## Planned Features
* [ ] RAG for realistic recommendations based on user situation (IKEA catalog, food blogs, etc.)
* [ ] Modern and nice frontend with react and typescript for __web__ 
* [ ] Modern and nice frontend with react-native for __mobile__
* [ ] Extend frontend with user session managment
* [ ] Improve API in backend for authentification
* [ ] Improve API security 
* [ ] Improve data model (relations) and API routes (retrievel by object ids) -> user can search and read old analysis and images/photos
* [ ] Implement a recommendation response as generated image based on recommendation text and uploaded image(s) as premium feature
* [ ] Brain storming for features as pro and premium features

---

## 📄 License

This project is currently under **development** and released as open source under the **MIT License**.

---

## 🙌 Credits

InspAIre is designed to help users discover the full potential of their environments using the power of personalized, explainable AI. Built with ❤️ by humans, enhanced by agents.