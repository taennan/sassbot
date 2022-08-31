<script lang="ts">
  import { onMount } from "svelte";
  import type { DOMRect } from "../lib/types";

  export let variant: "normal" | "good" | "bad" | "unsure" = "normal";
  //
  export let text: string;
  export let maxWidth: number = 250;
  export let minWidth: number = 50;

  export let lineOffset = 0;
  export let lineWidth = 10;
  export let lineHeight = 20;
  export let face: "left" | "right" | "down" = "down";

  // Bound <p> element
  let p: HTMLElement;
  let pRect: DOMRect | null = null;

  onMount(() => {
    pRect = p.getBoundingClientRect();
  });

  $: borderColour = (() => {
    switch (variant) {
      case "normal":
        return "#7d7d7d";
      case "good":
        return "green";
      case "unsure":
        return "yellow";
      case "bad":
        return "red";
    }
  })();

  $: w = pRect?.width ?? 0;

  $: lineLeftBase = w / 2 - lineWidth / 2 + w * lineOffset;
  $: lineRightBase = w / 2 + lineWidth / 2 + w * lineOffset;
  $: lineOrigin = (() => {
    switch (face) {
      case "left":
        return lineLeftBase;
      case "right":
        return lineRightBase;
      case "down":
        return (lineRightBase - lineLeftBase) / 2 + lineLeftBase;
    }
  })();
</script>

<div>
  <p
    bind:this={p}
    style:max-width="{maxWidth}px"
    style:min-width="{minWidth}px"
    style:--border-colour={borderColour}
  >
    {text}
  </p>
  <svg width={w} height={lineHeight}>
    <!--Left Speech Line-->
    <line x1={lineLeftBase} y1={0} x2={lineOrigin} y2={lineHeight} />
    <!--Right Speech Line-->
    <line x1={lineRightBase} y1={0} x2={lineOrigin} y2={lineHeight} />
  </svg>
</div>

<style lang="scss">
  @use "../styles/colours.scss";
  @use "../styles/sizes.scss";

  $padding-h: 6px;
  $padding-w: 7px;

  p {
    margin: 0;
    border: sizes.$border-width solid var(--border-colour);
    border-radius: sizes.$border-radius;
    padding: $padding-h $padding-w $padding-h $padding-w;
    color: colours.$primary-text;
    text-align: center;
    background-color: white;
  }

  line {
    stroke: colours.$speech-line-border;
    stroke-width: sizes.$border-width;
    stroke-linejoin: round;
    fill: white;
  }
</style>
