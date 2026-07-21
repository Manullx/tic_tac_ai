'use client'
import { Play, Player } from "@/app/lib/interfaces";
import { useState, ReactNode, useEffect } from "react";
import { createGame, getGame, postPlay } from "@/app/lib/api";

import Square from "@/app/components/square";


function FinishBanner({ finished, draw, winner }: { finished: boolean, draw: boolean, winner: Player | null }): ReactNode {
    
    if (!finished) {
        return <div className="h-10 w-60"></div>
    }

    if (draw) {
        
        return (<div className="flex justify-center items-center h-10 w-60 p-2 m-2 rounded-lg bg-gray-200">Empate</div>)
    }
    
    return (
        <div className="flex justify-center items-center h-10 w-60 p-2 m-2 rounded-lg text-white" style={{backgroundColor: winner == "X" ? "#C24242" : "#4282C2"}}>Ganhador { winner }</div>
    )
}

export default function Game() {
    
    const [ gameId, setGameId ] = useState<number>(0);
    const [ finishedState, setFinishedState ] = useState<boolean>(false);
    const [ winnerState, setWinnerState ] = useState<Player | null>(null);
    const [ drawState, setDrawState ] = useState<boolean>(false);

    const [ gameState, setGameState ] = useState<Array<Array<Play | null>>>([
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ]);
    

    useEffect( () => {

        const gameIdStorage = Number( localStorage.getItem("game_id") );
        
        if (gameIdStorage) {
            
            setGameId( gameIdStorage );
            
            getGame( { game_id: gameIdStorage } ).then( game => {
                
                setFinishedState( game.finished );
                setDrawState( game.draw );
                setWinnerState( game.winner );
                
                const newGameState = gameState.map( (row, row_i) => {
                    
                    const rowPlays = game.plays.filter( p => row_i == p.row );

                    if (rowPlays.length == 0) {

                        return row;
                    }

                    const newRow = [...row];

                    for ( const play of rowPlays ) {

                        newRow[ play.col ] = play;
                    }

                    return newRow
                });
                
                setGameState(newGameState);
            }).catch( _ => {
                
                createGame().then( game => {
            
                    localStorage.setItem("game_id", String(game.id) );
                    setGameId(game.id);
                });
            });

            return;
        } 
        
        createGame().then( game => {
            
            localStorage.setItem("game_id", String(game.id) );
            setGameId(game.id);
        });
    }, []);

    

    function handleClickSquare(playerRow: number, playerCol: number) {

        if (finishedState || gameState[playerRow][playerCol] != null) {

            return;
        }
        
        postPlay({ game_id: gameId, row: playerRow, col: playerCol }).then( data => {
            
            if (data.finished) {

                setFinishedState( data.finished );
                setDrawState( data.draw );

                if (data.winner) {

                    setWinnerState(data.winner);
                }
            }

            setGameState(currentGame => {
                const newGame = currentGame.map(row => [...row]);

                newGame[data.player_play.row][data.player_play.col] = data.player_play;

                if (data.agent_play) {
                    newGame[data.agent_play.row][data.agent_play.col] = data.agent_play;
                }

                return newGame;
            });
        })
    }
    
    function handleRefreshGame() {

        createGame().then( game => {

            setGameId(game.id);
            localStorage.setItem("game_id", String(game.id) );

            setFinishedState(game.finished);
            setDrawState(game.draw);
            setWinnerState(game.winner);

            setGameState([
                [null, null, null],
                [null, null, null],
                [null, null, null]
            ]);
        });
    }

    return (
        <div>

            <div className="flex items-center justify-center">
                <FinishBanner finished={finishedState} draw={drawState} winner={winnerState}/>
            </div>

            <div className="grid grid-cols-3 bg-gray-200 rounded-lg p-1">
                {
                    gameState.map( ( row, row_i ) => {
                        
                        return row.map( ( _, col_i ) => {
                            return <Square key={`${row_i}_${col_i}`} boardGameState={gameState} squareRow={row_i} squareCol={col_i} handleClickSquare={handleClickSquare}/>
                        })
                    })
                }
            </div>

            <div className="flex items-center justify-center">
                <button type="button" className="flex items-center justify-center rounded-lg bg-gray-200 hover:bg-gray-300 w-10 h-10 m-2" onClick={handleRefreshGame}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="size-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                    </svg>
                </button>
            </div>
        </div>
    )
}
