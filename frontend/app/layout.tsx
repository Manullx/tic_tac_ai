import "@/app/globals.css";

import React from "react";
import Image from "next/image";
import Link from "next/link";

import Navigation from "./components/navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>
                <header className="flex flex-row shadow-md">

                    <div className="flex justify-start items-center basis-1/3 pl-10 gap-2">
                        <Image
                            src="/tic_tac_ai.svg"
                            alt="TicTacBot"
                            width={100}
                            height={50}
                        />

                        <h1 className="font-bold">Tic Tac AI</h1>
                    </div>
                    <div className="flex justify-center items-center basis-1/3">
                        <Navigation />
                    </div>
                    <div className="flex justify-end items-center basis-1/3">
                        <a className="pr-10" href="https://github.com/Manullx/tic_tac_ai" target="_black">
                            <svg className="bg-white" viewBox="0 0 24 24" height={30} width={30}>
                                <path d="M10.226 17.284c-2.965-.36-5.054-2.493-5.054-5.256 0-1.123.404-2.336
                                1.078-3.144-.292-.741-.247-2.314.09-2.965.898-.112 2.111.36 2.83 1.01.853-.269
                                1.752-.404 2.853-.404 1.1 0 1.999.135 2.807.382.696-.629 1.932-1.1 2.83-.988.315.606.36 2.179.067
                                2.942.72.854 1.101 2 1.101 3.167 0 2.763-2.089 4.852-5.098 5.234.763.494 1.28 1.572 1.28
                                2.807v2.336c0 .674.561 1.056 1.235.786 4.066-1.55 7.255-5.615 7.255-10.646C23.5 6.188 18.334
                                1 11.978 1 5.62 1 .5 6.188.5 12.545c0 4.986 3.167 9.12 7.435 10.669.606.225 1.19-.18
                                1.19-.786V20.63a2.9 2.9 0 0 1-1.078.224c-1.483 0-2.359-.808-2.987-2.313-.247-.607-.517-.966-1.034-1.033-.27-.023-.359-.135-.359-.27
                                0-.27.45-.471.898-.471.652 0 1.213.404 1.797 1.235.45.651.921.943 1.483.943.561 0 .92-.202 1.437-.719.382-.381.674-.718.944-.943" />
                            </svg>
                        </a>
                    </div>
                </header>
                <main className="flex justify-center items-center h-screen">{ children }</main>
            </body>
        </html>
    )
}