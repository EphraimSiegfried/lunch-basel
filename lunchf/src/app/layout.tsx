import type { Metadata } from "next";
import LocalFont from "next/font/local";
import "./globals.css";

const geistSans = LocalFont({
  variable: "--font-geist-sans",
  src: "geist.woff2",
  display: "optional",
  preload: false
});

const geistMono = LocalFont({
  variable: "--font-geist-mono",
  src: "geist-mono.woff2",
  display: "optional",
  preload: false
});

export const metadata: Metadata = {
  title: "Basel Zmittag",
  description: "Was gits z'esse?",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
