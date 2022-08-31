<script lang="ts">
  import Button from "@smui/button";
  import CircularProgress from "@smui/circular-progress";
  import Animations from "./components/Animations.svelte";
  import TextCycle from "./components/TextCycle.svelte";
  import GreetingInput from "./components/GreetingInput.svelte";
  import ResponseInfo from "./components/ResponseInfo.svelte";
  import PerformanceInput from "./components/PerformanceInput.svelte";
  import Space from "./components/Space.svelte";
  import Center from "./components/Center.svelte";

  import { fly } from "svelte/transition";
  import { tips } from "./lib/utils";

  import type { ServerResponseJson } from "./lib/types";

  //
  let serverResponse: ServerResponseJson | null = null;
  //
  $: humanText = serverResponse ? serverResponse.input : "";
  $: robotText = serverResponse ? serverResponse.output : "";

  // Just for the initial fade-in as setting
  // a delay directly doesn't seem to work
  let hidden = true;
  setTimeout(() => {
    hidden = false;
  }, 300);
  //
  let showRespInfo = false;
  let textCanCycle = false;

  const activeSections = {
    animations: false,
    loader: false,
    greetingInput: true,
    performanceInput: false,
    responseInfo: false,
  };

  function handleRequestWillSend() {
    activeSections.loader = true;
    activeSections.animations = false;
    activeSections.performanceInput = false;
    activeSections.responseInfo = false;
  }

  async function handleServerResponded(event: CustomEvent<ServerResponseJson>) {
    textCanCycle = true;
    activeSections.loader = false;
    activeSections.animations = true;
    activeSections.performanceInput = true;
    activeSections.responseInfo = true;

    serverResponse = event.detail;
    console.log(`Server Response:`, serverResponse);
  }

  function handlePerformanceSent(_event: CustomEvent) {
    activeSections.performanceInput = false;
  }

  function handleToggleRespInfo() {
    showRespInfo = !showRespInfo;
  }
</script>

{#if !hidden}
  {@const flyOpts = { y: 40, duration: 300 }}
  {@const sectionSpacing = "xl"}
  <main>
    {#if activeSections.animations}
      <Center>
        <Animations {humanText} {robotText} />
      </Center>

      <Space size={sectionSpacing} />
    {/if}

    {#if activeSections.loader}
      <Center>
        <CircularProgress style="height: 50px; width: 50px" indeterminate />
      </Center>

      <Space size={sectionSpacing} />
    {/if}

    <div in:fly={flyOpts}>
      <TextCycle
        cycleTime={7 * 1000}
        text={textCanCycle ? tips() : ["Start by entering a polite greeting"]}
      />

      <Space />

      <GreetingInput
        initialValue="Hello, "
        on:requestWillSend={handleRequestWillSend}
        on:serverResponded={handleServerResponded}
      />

      <Space size={sectionSpacing} />
    </div>

    {#if activeSections.performanceInput}
      <!--Need to set fly as flip doesn't seem to work on dismount-->
      <div transition:fly={flyOpts}>
        <PerformanceInput on:performanceSent={handlePerformanceSent} />

        <Space size={sectionSpacing} />
      </div>
    {/if}

    {#if activeSections.responseInfo}
      <!--Need to set fly as flip doesn't seem to work on dismount-->
      <div transition:fly={flyOpts}>
        <Center>
          <Button variant="outlined" on:click={handleToggleRespInfo}>
            {showRespInfo ? "Hide Info" : "Show Info"}
          </Button>
        </Center>

        <Space />

        {#if showRespInfo}
          <div transition:fly={flyOpts}>
            <Center>
              <ResponseInfo {serverResponse} />
            </Center>
          </div>
        {/if}
      </div>
    {/if}
  </main>
{/if}

<style lang="scss">
  @use "./styles/globals.scss";

  main {
    $margin: 6em;
    margin-top: $margin;
    margin-bottom: $margin;
  }
</style>
