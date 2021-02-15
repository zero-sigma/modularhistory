import Head from "next/head";
import { useRouter } from "next/router";
// import Modal from "./modal";
import React from 'react';
import Footer from "./footer";
import Navbar from "./navbar";


export default function Layout({title, canonicalUrl, children}) {
  const router = useRouter();

  return (
    <>
      <Head>
        <title>{title || "Home"} | ModularHistory</title>
        <link rel="canonical" href={canonicalUrl || router.pathname} />
      </Head>

      <Navbar />

      <div className="main-content">
        {children}
      </div>

      <Footer />
      {/*<Modal />*/}
      {/* Removed scripts template tag.
          Can be added to Head with defer attribute */}
    </>
  );
}
