<script lang="ts">
  import Textfield from "@smui/textfield";
  import Button, { Label } from "@smui/button";
  import Space from "./Space.svelte";
  import Center from "./Center.svelte";

  import { createEventDispatcher } from "svelte";
  import {
    fetchResponse, // <-- For real
    fetchFakeResponse, // <-- For testing
  } from "../lib/server";

  export let initialValue: string = "";

  const dispatch = createEventDispatcher();

  let queryingServer = false;
  let value: string = initialValue;
  let lastValue: string | null = null;
  $: canSendRequest =
    !queryingServer && value !== lastValue && value.replaceAll(" ", "") !== "";

  async function sendRequest() {
    if (!canSendRequest) return;
    queryingServer = true;
    lastValue = value;

    dispatch("requestWillSend", value);

    //const detail = await fetchResponse(value);
    const detail = await fetchFakeResponse(value);
    dispatch("serverResponded", detail);
    queryingServer = false;
  }
</script>

<main>
  <Center>
    <Textfield
      style="width: 50%;"
      disabled={queryingServer}
      variant="outlined"
      label="Enter Greeting"
      bind:value
    />
  </Center>

  <Space />

  <Center>
    <Button variant="raised" disabled={!canSendRequest} on:click={sendRequest}>
      <Label>Send Greeting</Label>
    </Button>
  </Center>
</main>
