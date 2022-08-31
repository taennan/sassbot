<script lang="ts">
  /*
    Intended Usage:
    <Space w|h size="xl" />
   */

  type Size = "sm" | "md" | "lg" | "xl" | number;

  export let w: boolean = false;
  export let size: Size = "md";

  const isWidth = w ? w : false;
  const sizes = {
    sm: 10,
    md: 15,
    lg: 20,
    xl: 25,
  };
  $: spacing = sizes[size] ?? size;
</script>

{#if isWidth}
  <div style:width="{spacing}px" />
{:else}
  <div style:height="{spacing}px" />
{/if}
