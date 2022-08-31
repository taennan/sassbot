import { toCamel } from "snake-camel"

import type { RawServerResponseJson, ServerResponseJson } from "./types"

const PORT = import.meta.env.VITE_PORT
const URL = `http://localhost:${PORT}`

export async function fetchResponse(input: string): Promise<ServerResponseJson> {
  const url = `${URL}/sass/${input}`
  const res = await fetch(url)

  const rawResp: RawServerResponseJson = await res.json()
  const cmlResp = toCamel(rawResp) as ServerResponseJson

  return cmlResp
}

// Just for testing
export async function fetchFakeResponse(input: string): Promise<ServerResponseJson> {
  return new Promise((res, _) => {
    setTimeout(() => {
      res({
        input,
        output: "TODO",
        isPolite: false,
        prediction: 0.5,
        predictionTime: 0.0,
      })
    }, 2 * 1000)
  })
}
