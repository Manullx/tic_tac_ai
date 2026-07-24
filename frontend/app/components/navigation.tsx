'use client'
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navigation() {

    const pathName = usePathname()

    return (
        <nav className="flex gap-4">
            <Link className={`font-bold px-2 ${ pathName == "/" ? "border-b-2" : ""}`} href={"/"}>Game</Link>
            <Link className={`font-bold px-2 ${ pathName == "/dashboard" ? "border-b-2" : ""}`} href={"/dashboard"}>Dashboard</Link>
        </nav>
    )
}