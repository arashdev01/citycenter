import Link from "next/link";

async function getShops() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/shops/", {
      cache: "no-store",
    });
    return res.json();
  } catch {
    return [];
  }
}

export default async function Home() {
  const shops = await getShops();

  return (
    <main className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold text-emerald-400 mb-6">
        پاساژ
      </h1>

      {shops.length === 0 ? (
        <p>هیچ مغازه‌ای پیدا نشد.</p>
      ) : (
        <ul className="space-y-4">
          {shops.map((shop: any) => (
            <li key={shop.id} className="bg-slate-800 p-4 rounded">
              <Link href={`/shops/${shop.unit_number}`}>
                <h2 className="text-xl font-bold text-emerald-400 hover:underline cursor-pointer">
                  {shop.name}
                </h2>
              </Link>
              <p>واحد: {shop.unit_number}</p>
              <p>{shop.description}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}