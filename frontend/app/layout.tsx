import "@/app/globals.css";

import React from "react";
import Image from "next/image";

export default function GameLayout({ children, }: { children: React.ReactNode}) {
    return (
        <html lang="en">
            <body>
                <header className="flex justify-start items-center">

                    <Image
                        className="mr-4"
                        src="/tic_tac_ai.svg"
                        alt="TicTacBot"
                        width={100}
                        height={50}
                    />

                    <h1 className="font-bold">Tic Tac AI</h1>
                    
                </header>
                <main className="flex justify-center items-center h-screen">{ children }</main>
            </body>
        </html>
    )
} 