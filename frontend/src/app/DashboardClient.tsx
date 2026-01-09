'use client';

import { useState } from 'react';
import { UpdateItem } from '@/lib/types';
import { format } from 'date-fns';
import { ExternalLink } from 'lucide-react';

interface Props {
    updates: UpdateItem[];
    sources: string[];
}

export default function DashboardClient({ updates, sources }: Props) {
    const [selectedSource, setSelectedSource] = useState<string>('All');

    const filteredUpdates = selectedSource === 'All'
        ? updates
        : updates.filter(u => u.source === selectedSource);

    return (
        <div>
            {/* Filter Bar */}
            <div className="flex flex-wrap gap-2 mb-8 border-b border-slate-100 pb-4">
                <button
                    onClick={() => setSelectedSource('All')}
                    className={`px-4 py-2 text-sm font-medium rounded-full transition-colors ${selectedSource === 'All'
                            ? 'bg-slate-900 text-white'
                            : 'bg-white text-slate-500 hover:bg-slate-50 border border-slate-200'
                        }`}
                >
                    All
                </button>
                {sources.map(source => (
                    <button
                        key={source}
                        onClick={() => setSelectedSource(source)}
                        className={`px-4 py-2 text-sm font-medium rounded-full transition-colors ${selectedSource === source
                                ? 'bg-slate-900 text-white'
                                : 'bg-white text-slate-500 hover:bg-slate-50 border border-slate-200'
                            }`}
                    >
                        {source}
                    </button>
                ))}
            </div>

            {/* Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {filteredUpdates.length === 0 ? (
                    <div className="col-span-full text-center py-20 text-slate-400">
                        No updates found for this selection.
                    </div>
                ) : (
                    filteredUpdates.map((update) => (
                        <article
                            key={update.id}
                            className="group bg-white border border-slate-200 p-6 rounded-lg hover:border-slate-400 transition-all flex flex-col h-full"
                        >
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 border border-slate-100 px-2 py-1 rounded">
                                    {update.source}
                                </span>
                                <time className="text-xs text-slate-400">
                                    {format(new Date(update.date), 'yyyy.MM.dd')}
                                </time>
                            </div>

                            <h2 className="text-lg font-bold mb-3 leading-tight group-hover:text-blue-600 transition-colors">
                                <a href={update.url} target="_blank" rel="noopener noreferrer">
                                    {update.title}
                                </a>
                            </h2>

                            <p className="text-sm text-slate-600 mb-6 flex-grow whitespace-pre-line leading-relaxed">
                                {update.summary || 'No summary available.'}
                            </p>

                            <div className="pt-4 border-t border-slate-50 mt-auto">
                                <a
                                    href={update.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center text-xs font-medium text-slate-900 hover:underline"
                                >
                                    Source <ExternalLink className="w-3 h-3 ml-1" />
                                </a>
                            </div>
                        </article>
                    ))
                )}
            </div>
        </div>
    );
}
