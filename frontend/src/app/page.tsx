import updatesData from '@/data/updates.json';
import { UpdateItem } from '@/lib/types';
import { FilterBar } from '@/components/FilterBar'; // We will create this or inline it
import DashboardClient from './DashboardClient'; // Client component for interactivity

// Force static generation
export const dynamic = 'force-static';

export default function Home() {
    // Sort by date desc
    const updates = (updatesData as UpdateItem[]).sort((a, b) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
    );

    // Extract unique sources
    const sources = Array.from(new Set(updates.map(u => u.source)));

    return (
        <main className="min-h-screen bg-white text-slate-900 p-4 md:p-8 max-w-5xl mx-auto">
            <header className="mb-12 mt-4 space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Ad Platform Updates</h1>
                <p className="text-slate-500 text-sm">Daily Design & Tech Updates • Automated</p>
            </header>

            <DashboardClient updates={updates} sources={sources} />
        </main>
    );
}
