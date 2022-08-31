
export interface Position {
  x: number,
  y: number,
}
export interface Size {
  height: number,
  width: number,
}
export interface DOMRect extends Position, Size {
  bottom: number,
  top: number,
  left: number,
  right: number,
}

export interface RawServerResponseJson {
  input: string,
  output: string,
  is_polite: boolean,
  prediction: number,
  prediction_time: number,
}
export interface ServerResponseJson {
  input: string,
  output: string,
  isPolite: boolean,
  prediction: number,
  predictionTime: number,
}
