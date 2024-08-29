import * as React from "react";
import * as HomeController from "./_server";
import { createServerPage } from "@/components/ServerPages";

const HomePage = createServerPage(HomeController);
const Home = () => {
  return (
    <div className="p-6 bg-black">
      <div className="flex justify-between items-center mb-4">
        hello world
      </div>
    </div>
  );
};

export default HomePage.wraps(Home);
