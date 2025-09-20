import Head from 'next/head';

type Menu = {
  title: string;
  ingredients: string;
};

type Restaurant = {
  name: string;
  url: string;
};

type LunchOffer = {
  restaurant: Restaurant;
  menus: Menu[];
};

async function getLunchOffers(): Promise<LunchOffer[]> {
  const API_BASE_URL = process.env.API_BASE_URL || "http://backend:8218";

  try {
    const restaurantsRes = await fetch(`${API_BASE_URL}/list-restaurants`, { cache: 'no-store' });
    if (!restaurantsRes.ok) throw new Error("Failed to fetch restaurants");

    const restaurants: Restaurant[] = await restaurantsRes.json();
    const menuPromises = restaurants.map(async (restaurant) => {
    const menuRes = await fetch(
      `${API_BASE_URL}/menu/${encodeURIComponent(restaurant.name)}/today`,
      { cache: 'no-store' }
    );
      const menus: Menu[] = menuRes.ok ? await menuRes.json() : [];
      return { restaurant, menus };
    });

    return await Promise.all(menuPromises);
  } catch (error) {
    console.error("Error fetching lunch offers:", error);
    return [];
  }
}

export default async function Home() {
  let lunchOffers = await getLunchOffers();
  lunchOffers = lunchOffers.filter((o) => o.menus.length != 0)

  return (
    <div className="bg-gray-100 min-h-screen p-4 sm:p-8 font-sans">
      <Head>
        <title>Zmittag</title>
      </Head>
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 mb-8 text-center">
	  Zmittag
        </h1>
        {lunchOffers.length === 0 ? (
          <p className="text-center text-gray-500 text-xl">
            Could not load any lunch offers at the moment. Please try again later.
	    No menus today!
          </p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {lunchOffers.map((offer, index) => (
              <div
                key={index}
                className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 p-6 flex flex-col"
              >
                <a
                  href={offer.restaurant.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-2xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200 mb-4"
                >
                  {offer.restaurant.name}
                </a>
                <div className="space-y-4 flex-grow">
                  {offer.menus.map((menu, menuIndex) => (
                    <div key={menuIndex} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-700 mb-1">
                        {menu.title}
                      </h3>
                      <p className="text-gray-500">
                        <span className="font-medium text-gray-600"></span> {menu.ingredients}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
