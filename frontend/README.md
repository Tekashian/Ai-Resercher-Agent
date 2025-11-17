# AI Research Agent - Frontend

Modern, animated React frontend for the AI Research Agent powered by Google Gemini 2.5 Flash.

## 🎨 Features

- **Modern Design**: Gradient-based UI with glassmorphism effects
- **Smooth Animations**: Framer Motion for fluid transitions
- **Responsive**: Mobile-first design that works on all devices
- **Intuitive UX**: Clean interface focused on research workflow
- **Real-time Updates**: Live status updates during research
- **PDF Export**: Download professional research reports

## 🚀 Tech Stack

- React 18
- Framer Motion (animations)
- Axios (API calls)
- React Router (navigation)
- Lucide React (icons)
- React Markdown (content rendering)

## 📦 Installation

```bash
cd frontend
npm install
```

## 🏃 Running the App

Make sure the backend server is running on `http://localhost:8000`, then:

```bash
npm start
```

The app will open at `http://localhost:3000`

## 🎯 Usage

1. **Home Page**: Enter research topic and select number of sources
2. **Research Page**: View AI-generated analysis, findings, and sources
3. **History Page**: Browse past research with quick access
4. **PDF Export**: Download professional reports with one click

## 🎨 Design System

### Colors
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Accent: `#ec4899` (Pink)
- Success: `#10b981` (Green)
- Background: `#0a0e1a` (Dark Blue)

### Fonts
- Interface: Inter
- Code: JetBrains Mono

## 📱 Responsive Breakpoints

- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: < 768px

## 🔧 Configuration

The app uses a proxy to connect to the backend API:
```json
"proxy": "http://localhost:8000"
```

Change this in `package.json` if your backend runs on a different port.

## 🏗️ Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## 📄 License

MIT
