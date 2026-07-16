import { getGame } from "@/app/lib/game"

import Board from "@/app/components/board"

export default async function Game() {
  
  const { game_id } = { game_id: 0}

  return (
    <div>
      <div className="flex justify-center">
        game_id: { game_id }
      </div>
      <Board />
    </div>
  )
}