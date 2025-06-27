'use client';

import { useEffect, useState } from 'react';

interface ProvidersProps {
  children: React.ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Return a loading placeholder that matches the server-rendered content
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="animate-pulse">
          {/* Header skeleton */}
          <div className="bg-white shadow-sm border-b border-gray-200 h-16"></div>
          
          {/* Hero section skeleton */}
          <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 h-64">
            <div className="flex items-center justify-center h-full">
              <div className="text-white text-xl">Loading...</div>
            </div>
          </div>
          
          {/* Main content skeleton */}
          <div className="mx-auto max-w-7xl px-6 py-12">
            <div className="grid gap-8 lg:grid-cols-3">
              <div className="lg:col-span-1 space-y-6">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="rounded-xl bg-white p-6 shadow-lg border border-gray-100">
                    <div className="h-20 bg-gray-200 rounded"></div>
                  </div>
                ))}
              </div>
              <div className="lg:col-span-2">
                <div className="rounded-xl bg-white p-12 shadow-lg border border-gray-100">
                  <div className="h-64 bg-gray-200 rounded"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
