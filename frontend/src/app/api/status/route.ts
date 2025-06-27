import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5001';

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/status`);
    
    if (!response.ok) {
      throw new Error(`Backend responded with status ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Status API error:', error);
    
    // Return mock status when backend is not available
    return NextResponse.json({
      gemini: false,
      alphaVantage: false,
      newsApi: false,
      advancedCharts: false,
      pdfGeneration: false,
      error: 'Backend not available - using demo mode'
    });
  }
}