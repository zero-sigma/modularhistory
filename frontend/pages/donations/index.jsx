import Link from "next/link";
import React from "react";
import Layout from "../../components/layout";

export default function Donations() {
  return (
    <Layout>
      <div>
        <h1 className="p-4 display-3 text-center">DONATE</h1>
        <h4 className="m-2 text-center text-secondary">
          Modular history is a non-profit organization that helps people to learn about and understand history. Donate to our cause because learning can't wait.
        </h4>
        <p className="p-4 text-monospace text-center text-secondary">
          <Link href={'/donate-now'}>
            <button className="btn btn-primary active" type="button">Donate Now</button>
          </Link>
          {" "}
          <Link href={'/about/'}>
            <button className="btn btn-primary active" type="button">About</button>
          </Link>
        </p>
      </div>
    </Layout>
  );
}

