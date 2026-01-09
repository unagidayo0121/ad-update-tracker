# Daily Ad Platform Updates

Automated dashboard collecting daily updates from major advertising platforms (Google Ads, Yahoo! JAPAN, etc.), summarized by Gemini 1.5 Flash.

## Features
- **Automated Collection**: Runs daily via GitHub Actions.
- **AI Summarization**: Uses Gemini 1.5 Flash to filter implementation-level updates and summarize them in Japanese.
- **Minimalist Dashboard**: Clean, black & white UI built with Next.js and Tailwind CSS.
- **Data Archive**: All updates are stored in `data/updates.json`.

## Setup
### 1. Prerequisites
- GitHub Account
- Google Gemini API Key

### 2. Deployment
1. **Fork** or **Clone** this repository.
2. Go to **Settings > Secrets and variables > Actions**.
3. Create a **New repository secret**:
   - Name: `GOOGLE_API_KEY`
   - Value: (Your Gemini API Key)
4. Go to **Settings > Pages**.
   - Source: **GitHub Actions**
5. Enable the Workflow:
   - Go to **Actions** tab.
   - Select **Daily Ad Updates** workflow.
   - Click **Run workflow** to trigger the first run manually.

## Local Development
Since the project uses Next.js, you can run the frontend locally:

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run development server:
   ```bash
   npm run dev
   ```
   Access at `http://localhost:3000`.

## Architecture
- **Backend**: Python scripts (`backend/`) scrape RSS feeds and use Gemini API for content analysis.
- **Frontend**: Next.js app (`frontend/`) renders the static dashboard.
- **Data**: JSON storage (`data/updates.json`).
