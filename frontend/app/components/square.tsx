'use client'
import { Player, Play } from "@/app/lib/interfaces"
import { useEffect, useState } from "react";

export default function Square( { 
    boardGameState, squareRow, squareCol, handleClickSquare
 }: { 
    boardGameState: Array<Array<Play | null>>, squareRow: number, squareCol: number, handleClickSquare: any
  }) {

    if ( boardGameState[squareRow][squareCol] == null ) {
        
        return (
            <div 
                className = "flex justify-center items-center w-20 h-20 bg-white m-1 rounded-lg text-xl font-bold"
                onClick={ _ => handleClickSquare( squareRow, squareCol ) }
            >
            </div>
        )
    }
    
    return (
        <div 
            className = "flex justify-center items-center w-20 h-20 bg-white m-1 rounded-lg text-xl font-bold border-2"
            style = {{
                backgroundColor: boardGameState[squareRow][squareCol].player == "X" ? "#f0b5b5" : "#c1d2e2",
                borderColor: boardGameState[squareRow][squareCol].player == "X" ? "#C24242" : "#4282C2"
            }}
            onClick={ _ => handleClickSquare( squareRow, squareCol ) }
        >
            { boardGameState[squareRow][squareCol].player }
        </div>
    )
} 