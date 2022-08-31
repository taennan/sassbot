import shuffle from "lodash.shuffle"

export function tips(): string[] {

  const theFirst = [
    "Now try something impolite and see how SassBot responds!"
  ]
  const theRest = shuffle([
    "It's just a test, don't expect too much",
    "There is a 1000 character limit to the greetings you can send, so make it snappy!",
    "Try \"You're a loser SassBot!\" or \"SassBot, you are amazing!\"",
    "Introductions! Human, Machine. Machine, Human",
    "The algorithm has a 75% accuracy. It may respond incorrectly sometimes",
    "You don't have to type in a greeting, any old sentance will do",
    "Try sentances which aren't obviously polite or impolite, we might be surprised",
    "The use of emojis is definitely encouraged! ;)",
    "Most punctuation is removed by the algorithm... your exclaimation marks won't do anything",
    "Find the hidden button in the app and get a free pat on the back!"
    // Keep adding more!
  ])

  return theFirst.concat(theRest)
}

export function getElementHeight(element: HTMLElement): number {
  const height = element.getBoundingClientRect().height;

  const style = getComputedStyle(element);
  const marginTop = parseFloat(style.marginTop);
  const marginBtm = parseFloat(style.marginBottom);

  return height + marginBtm + marginTop;
}
