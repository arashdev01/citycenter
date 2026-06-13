async function getShop(unitNumber: string) {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/citycenter/${unitNumber}/`,
      { cache: "no-store" }
    );
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export default async function ShopPage({
  params,
}: {
  params: Promise<{ unit_number: string }>;
}) {
  const { unit_number } = await params;
  const shop = await getShop(unit_number);

  if (!shop) {
    return (
      <main className="min-h-screen bg-slate-900 text-white p-8">
        <p>مغازه پیدا نشد.</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold text-emerald-400 mb-4">
        {shop.name}
      </h1>
      <p className="mb-2">واحد: {shop.unit_number}</p>
      <p className="mb-6">{shop.description}</p>

      <h2 className="text-xl font-bold mb-3">محصولات</h2>
      {shop.products.length === 0 ? (
        <p>محصولی ثبت نشده.</p>
      ) : (
        <ul className="space-y-3">
          {shop.products.map((product: any) => (
            <li key={product.id} className="bg-slate-800 p-3 rounded">
              <p className="font-bold">{product.name}</p>
              <p>قیمت: {product.price} تومان</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}