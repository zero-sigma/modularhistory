import { DJANGO_CSRF_COOKIE_NAME } from "@/auth";
import axiosWithoutAuth from "@/axiosWithoutAuth";
import { PageTransitionContextProvider } from "@/components/PageTransitionContext";
import { initializeSentry } from "@/sentry";
import "@/styles/globals.css";
import { createTheme, StyledEngineProvider, ThemeProvider } from "@material-ui/core/styles";
import { StylesProvider } from "@material-ui/styles";
import { NextPage } from "next";
import { Provider, signOut, useSession } from "next-auth/client";
import { AppProps } from "next/app";
import Head from "next/head";
import { FC, ReactElement, useEffect } from "react";
import Cookies from "universal-cookie";
import "../../core/static/styles/base.scss";

initializeSentry();

const cookies = new Cookies();

const theme = createTheme({});

interface SessionKillerProps {
  children: ReactElement;
}

const SessionKiller: FC<SessionKillerProps> = ({ children }: SessionKillerProps) => {
  const [session, _loading] = useSession();
  useEffect(() => {
    if (session?.expired) {
      signOut();
    }
  }, [session?.expired]);
  return children;
};

interface ExtendedAppProps extends AppProps {
  err?: string;
}

const App: NextPage<AppProps> = ({ Component, pageProps, err }: ExtendedAppProps) => {
  useEffect(() => {
    // Remove the server-side injected CSS.
    // See https://github.com/mui-org/material-ui/blob/master/examples/nextjs/.
    const jssStyles = document.querySelector("#jss-server-side");
    if (jssStyles) {
      jssStyles.parentElement.removeChild(jssStyles);
    }

    // Set the Django CSRF cookie if necessary.
    if (!cookies.get(DJANGO_CSRF_COOKIE_NAME)) {
      // Get Django CSRF cookie.
      // eslint-disable-next-line no-console
      const url = "/api/csrf/set/";
      axiosWithoutAuth.get(url);
    }
  }, []);

  return (
    <>
      <Head>
        {/*<title>Home | ModularHistory</title>*/}
        <meta charSet="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta httpEquiv="Content-Language" content="en" />
        <meta property="og:type" content="website" />
        {/* TODO: Use a better image. (This is the image that appears
                  in messaging apps when a link to the website is shared.) */}
        {/*<meta property="og:image" content="{% static 'logo_head_white.png' %}" />*/}
        <meta property="og:url" content="https://www.modularhistory.com/" />
        <meta property="og:title" content="ModularHistory" />
        <meta property="og:description" content="History, modularized." />
        <meta name="facebook-domain-verification" content="dfnrpkj6k5hhiqtxmtxsgw23xr8bfr" />
      </Head>
      <noscript>
        <iframe
          src="https://www.googletagmanager.com/ns.html?id=GTM-P68V7DK"
          height="0"
          width="0"
          style={{ display: "none", visibility: "hidden" }}
        />
      </noscript>
      <Provider session={pageProps.session}>
        <SessionKiller>
          <PageTransitionContextProvider>
            <StyledEngineProvider injectFirst>
              <StylesProvider>
                <ThemeProvider theme={theme}>
                  <Component {...pageProps} err={err} />
                </ThemeProvider>
              </StylesProvider>
            </StyledEngineProvider>
          </PageTransitionContextProvider>
        </SessionKiller>
      </Provider>
    </>
  );
};

export default App;
