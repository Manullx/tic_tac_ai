'use client'

export default function Square( { boardGameState, squareRow, squareCol, handleClickSquare }: { boardGameState: Array<Array<string | null>>, squareRow: number, squareCol: number, handleClickSquare: any }) {

    let squareColor;
    if (boardGameState[squareRow][squareCol] != null) {
        
        squareColor = boardGameState[squareRow][squareCol] == "X" ? "#C24242" : "#4282C2";
    }

    return (
        <div 
            className="flex justify-center items-center w-20 h-20 bg-white m-1 rounded-lg text-xl font-bold"
            style={{borderColor: squareColor, backgroundColor: squareColor}}
            onClick={ _ => handleClickSquare( squareRow, squareCol ) }
        >
            { boardGameState[squareRow][squareCol] }
        </div>
    )
} 