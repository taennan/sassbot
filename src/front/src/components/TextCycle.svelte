<script lang="ts">
  import { fly } from "svelte/transition";
  import { getElementHeight } from "../lib/utils";

  export let text: string[];
  export let cycle: boolean = true;
  export let cycleTime: number;

  export let fadeTime: number = 300;
  export let fadeDistanceX: number = 0;
  export let fadeDistanceY: number = 20;

  //
  let p: HTMLElement | undefined;
  $: totalHeight = p ? getElementHeight(p) : 50;

  // The index of the currently shown text
  // - Is incremented every 'cycleTime' milliseconds
  let i = 0;
  setInterval(() => {
    if (cycle) i = (i + 1) % text.length;
  }, cycleTime);
</script>

<div style:height="{totalHeight}px">
  {#each text as t, ii}
    {#if ii === i}
      <p
        bind:this={p}
        in:fly={{ x: -fadeDistanceX, y: -fadeDistanceY, duration: fadeTime }}
        out:fly={{ x: fadeDistanceX, y: fadeDistanceY, duration: fadeTime }}
      >
        {t}
      </p>
    {/if}
  {/each}
</div>

<style lang="scss">
  div {
    display: flex;
    justify-content: center;
  }

  p {
    text-align: center;
    max-width: 500px;
    position: absolute;
  }
</style>
