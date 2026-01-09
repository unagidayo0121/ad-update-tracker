import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#ffffff", // White
                foreground: "#0f172a", // Slate-900 for text (almost black but softer)
                border: "#e2e8f0", // Light gray for borders
                card: "#ffffff",
                "card-foreground": "#0f172a",
                muted: "#f1f5f9",
                "muted-foreground": "#64748b",
            },
        },
    },
    plugins: [],
};
export default config;
