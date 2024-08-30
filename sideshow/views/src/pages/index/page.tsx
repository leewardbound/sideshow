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
        <Title />
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
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {result.tokens.map((token) => (
                  <TokenRow key={token.address} {...token} />
                ))}
              </tbody>
            </table>
      </div>
    </div>
    </div>
  );
};

function TokenRow(token: HomeController.TokenOutput) {
  function latestValue(type: "open" | "close" | "high" | "low" | "priceUSD") {
    const data = token.chartData?.[type]
    const latestNonzero = data?.reverse().find(([_, __, value]) => value !== 0)
    if (!latestNonzero) {
      return 0;
    }
    return latestNonzero[2];
  }
  return (
    <tr key={token.address}>
      <td className="px-6 py-4 whitespace-nowrap">{token.name}</td>
      <td className="px-6 py-4 whitespace-nowrap">{token.symbol}</td>
      <td className="px-6 py-4 whitespace-nowrap">{formatUSD(token.volumeUSD)}</td>
      <td className="px-6 py-4 whitespace-nowrap">{Math.round(Number(token.totalSupply)).toLocaleString()}</td>
      <td className="px-6 py-4 whitespace-nowrap">{formatUSD(latestValue("priceUSD"))}</td>
    </tr>
  );
}

function Title() {
  return (
    <>
    <h1 className="text-2xl font-bold text-gray-200">
      {"Sideshow".split("").map((letter, index) => (
        <span key={index} className="animate-glow" style={{ animationDelay: `${index * 0.1}s` }}>
              {letter}
            </span>
          ))}
        </h1>
        <style>{`
          @keyframes glow {
            0% { text-shadow: 0 0px 15px red; }
            14% { text-shadow: 0 0px 15px orange; }
            28% { text-shadow: 0 0px 15px yellow; }
            42% { text-shadow: 0 0px 15px green; }
            57% { text-shadow: 0 0px 15px blue; }
            71% { text-shadow: 0 0px 15px indigo; }
            85% { text-shadow: 0 0px 15px violet; }
            100% { text-shadow: 0 0px 15px red; }
          }
          .animate-glow {
            animation: glow 5s infinite;
          }
        `}</style>
      </>
  );
}

function formatUSD(value: number | string) {
  const num = Number(value)
  if (num < 1 && num > 0) {
    return (num * 100).toFixed(4) + ' cents';
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(value));
}

export default HomePage.wraps(Home);
