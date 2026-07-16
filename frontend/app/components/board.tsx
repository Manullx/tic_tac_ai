'use client'

import Square from "@/app/components/square";
import { useState, ReactNode } from "react";

import { postPlay } from "@/app/lib/api";

function FinishBanner({ finshed, draw, winner }: { finshed: boolean, draw: boolean, winner: string | null }): ReactNode {
    
    if (!finshed) {
        return <></>
    }

    if (draw) {
        
        return (<div className="flex justify-center items-center p-2 m-2 rounded-lg bg-gray-200">Empate</div>)
    }
    
    return (
        <div className="flex justify-center items-center p-2 m-2 rounded-lg text-white" style={{backgroundColor: winner == "X" ? "#C24242" : "#4282C2"}}>Ganhador { winner }</div>
    )
}

export default function Board({ game_id }: { game_id: number }) {

    const [ finishedState, setFinishedState ] = useState<boolean>(false);
    const [ winnerState, setWinnerState ] = useState<string | null>("");
    const [ drawState, setDrawState ] = useState<boolean>(false);
    const [ gameState, setGameState ]  = useState<Array<Array<string | null>>>([
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ]);

    function handleClickSquare(playerRow: number, playerCol: number) {

        if (finishedState) {
            return;
        }
        
        let newGame = gameState.map( (newRow, newRowIndex) => {
            
            if (playerRow != newRowIndex) {
                return newRow;
            }

            newRow[playerCol] = "X";

            return newRow;
        });
        
        setGameState(newGame);

        postPlay( game_id, playerRow, playerCol ).then( ({ finished, draw, winner, row, col }) => {

            newGame = gameState.map( (newRow, newRowIndex) => {
            
                if (row != newRowIndex) {
                    return newRow;
                }

                newRow[col] = "O";

                return newRow;
            });

            setGameState(newGame);

            if (finished) {

                if (draw) {

                    setDrawState(draw);
                }

                setWinnerState(winner);
                setFinishedState(finished);
            }
        });
    }

    return (
        <div>

            <FinishBanner finshed={finishedState} draw={drawState} winner={winnerState}/>

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