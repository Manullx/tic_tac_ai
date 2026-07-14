'use client'

import { useState } from "react";
import Square from "./square";
import { collectMeta } from "next/dist/build/utils";

export default function Board() {
    
    const [ gameState, setGameState ]  = useState<Array<Array<string | null>>>([
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ]);

    function handleClickSquare(player: string, row: number, col: number) {
        
        const newGame = gameState.map( (newRow, newRowIndex) => {
            
            if (row != newRowIndex) {
                return newRow;
            }

            newRow[col] = player;

            return newRow;
        });
        
        setGameState(newGame);
    }

    return (
        <div className="grid grid-cols-3 bg-gray-200 rounded-lg p-1">
            {
                gameState.map( (row, row_i) => {

                    return row.map( (sqr, col_i) => {
                        
                        return (
                            <Square 
                                boardGameState={gameState}
                                squareRow={row_i}
                                squareCol={col_i}
                                handleClickSquare={handleClickSquare}
                            />
                        )
                    } )
                } )
            }
        </div>
    )
}