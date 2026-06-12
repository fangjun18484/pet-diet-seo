import type { APIRoute } from 'astro';
import fs from 'node:fs';
import path from 'node:path';

export const prerender = false; // Ensure this route is evaluated on the server

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json();
    const { breedId, breedName, foodId, foodName } = data;

    if (!breedId || !foodId) {
      return new Response(JSON.stringify({ error: 'Missing data' }), { status: 400 });
    }

    const pendingFilePath = path.resolve('./data/pending.json');
    let pending = [];
    if (fs.existsSync(pendingFilePath)) {
      pending = JSON.parse(fs.readFileSync(pendingFilePath, 'utf-8'));
    }

    // Check if already in queue
    const exists = pending.find((item: any) => item.breedId === breedId && item.foodId === foodId);
    if (!exists) {
      pending.push({
        breedId,
        breedName: breedName || breedId.replace(/-/g, ' '),
        foodId,
        foodName: foodName || foodId.replace(/-/g, ' '),
        timestamp: new Date().toISOString()
      });
      fs.writeFileSync(pendingFilePath, JSON.stringify(pending, null, 2));
    }

    return new Response(JSON.stringify({ success: true, queued: !exists }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error' }), { status: 500 });
  }
};
