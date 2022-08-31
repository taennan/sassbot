<script lang="ts">
  import DataTable, { Body, Row, Cell } from "@smui/data-table";
  import Center from "./Center.svelte";
  import Space from "./Space.svelte";

  import type { ServerResponseJson } from "../lib/types";

  export let serverResponse: ServerResponseJson;

  $: items = [
    ["Politeness", serverResponse.isPolite ? "Polite" : "Impolite"],
    ["Prediction", serverResponse.prediction],
    ["Time Taken", serverResponse.predictionTime + "ms"],
  ];
</script>

<DataTable>
  <Body>
    {#each items as i}
      {@const label = i[0]}
      {@const value = i[1]}
      <Row>
        <Cell><strong>{label}</strong></Cell>
        <Cell>{value}</Cell>
      </Row>
    {/each}
  </Body>
</DataTable>
