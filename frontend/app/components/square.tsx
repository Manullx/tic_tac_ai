'use client'

export default function Square( { boardGameState, squareRow, squareCol, handleClickSquare }: { boardGameState: Array<Array<string>> | null, squareRow: number, squareCol: number, handleClickSquare: any }) {

    return (
        <div className="w-20 h-20 bg-white m-1 rounded-lg text-red-500" onClick={_ => handleClickSquare( "X", squareRow, squareCol )}>
            { boardGameState[squareRow][squareCol] }
        </div>
    )
}