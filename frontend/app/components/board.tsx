'use client'

import Square from "@/app/components/square";
import { useState } from "react";

import { postPlay } from "@/app/lib/api";

export default function Board({ game_id }: { game_id: number }) {

    const [ finishedGame, setFinishedGame ] = useState(null);
    const [ gameState, setGameState ]  = useState<Array<Array<string | null>>>([
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ]);

    async function handleClickSquare(playerRow: number, playerCol: number) {
        
        let newGame = gameState.map( (newRow, newRowIndex) => {
            
            if (playerRow != newRowIndex) {
                return newRow;
            }

            newRow[playerCol] = "X";

            return newRow;
        });
        
        setGameState(newGame);

        const { finished, winner, row, col } = await postPlay( game_id, playerRow, playerCol);
        
        newGame = gameState.map( (newRow, newRowIndex) => {
            
            if (row != newRowIndex) {
                return newRow;
            }

            newRow[col] = "O";

            return newRow;
        });

        setGameState(newGame);

        if (finished) {
            setFinishedGame(winner);
            return
        }
    }

    return (
        <div>
            { finishedGame ? <div className="flex justify-center items-center text-xg m-2">Ganhador: {finishedGame}</div> : ""}
            <div className="grid grid-cols-3 bg-gray-200 rounded-lg p-1">
                {
                    gameState.map( (row, row_i) => {

                        return row.map( (sqr, col_i) => {
                            
                            return (
                                <Square
                                    key={`${row_i}_${col_i}`}
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
        </div>
    )
}