import * as React from "react";
import * as HomeController from "./_server";
import { createServerPage } from "@/components/ServerPages";

const HomePage = createServerPage(HomeController);
const Home = () => {
  const result = HomePage.useContext();
  return (
    <div>
    <div className="p-6 bg-black">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Sideshow</h1>
      </div>
    </div>
    <div className="p-6">
        <div className="flex justify-between items-center mb-4">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Symbol</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Supply</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {result.tokens.map((token) => (
                  <tr key={token.address}>
                    <td className="px-6 py-4 whitespace-nowrap">{token.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{token.symbol}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{formatUSD(token.volumeUSD)}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{Math.round(Number(token.totalSupply)).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
      </div>
    </div>
    </div>
  );
};

function formatUSD(value: number | string) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(value));
}

export default HomePage.wraps(Home);
