(function testCircularBufferArray() {
  console.log("Starting CircularBufferArray tests...");

  const buffer = new CircularBufferArray(5);
  console.assert(
    buffer.maxSize === 5,
    "Failed: Buffer initialized with incorrect maxSize."
  );

  // Test pushing data
  buffer.push("A");
  buffer.push("B");
  buffer.push("C");
  console.assert(
    buffer.read() === "A",
    "Failed: First read did not return the oldest data."
  );

  // Advance readIndex and test reading next item
  buffer.advanceReadIndex(1);
  console.assert(
    buffer.read() === "B",
    "Failed: Read did not advance to next oldest item correctly."
  );

  // Test overwriting data and ensuring readIndex updates to oldest available data
  buffer.push("D");
  buffer.push("E");
  buffer.push("F"); // Overwrites "A"
  buffer.push("G"); // Overwrites "B", readIndex should now point to "C"
  console.assert(
    buffer.read() === "C",
    "Failed: Buffer did not update readIndex correctly on overwrite."
  );

  // Test advancing readIndex without going beyond newest data

  buffer.advanceReadIndex(3); // Should advance to "F"

  console.assert(
    buffer.read() === "F",
    "Failed: advanceReadIndex did not advance correctly or exceeded buffer bounds."
  );

  // Test rewinding readIndex
  buffer.rewindReadIndex(2); // Rewind back to "D"
  console.assert(
    buffer.read() === "D",
    "Failed: rewindReadIndex did not rewind correctly. D"
  );

  // Fill buffer and test boundary conditions
  buffer.push("H"); // Overwrites "C"
  buffer.push("I"); // Overwrites "D"
  buffer.advanceReadIndex(100); // Try to advance well beyond newest data
  console.assert(
    buffer.read() === "I",
    "Failed: Buffer allowed advancing beyond newest data."
  );
  buffer.rewindReadIndex(100); // Try to rewind well before the oldest data
  console.assert(
    buffer.read() === "E",
    "Failed: Buffer allowed rewinding beyond oldest data. E"
  );

  console.log("CircularBufferArray tests completed.");
})();

console.log("MORE TESTS");
(function testCircularBufferArrayEdgeCases() {
  console.log("Starting CircularBufferArray edge case tests...");

  const buffer = new CircularBufferArray(3);
  console.assert(
    buffer.maxSize === 3,
    "Buffer initialized with incorrect maxSize."
  );

  // Rapid fill and read all
  buffer.push("1");
  buffer.push("2");
  buffer.push("3");
  console.assert(
    buffer.read() === "1",
    "Failed: Incorrect data on first full read."
  );

  // Advance readIndex to the end and attempt to go beyond
  buffer.advanceReadIndex(2); // Move readIndex to beyond the last item
  console.assert(
    buffer.read() === "3",
    "Failed: Did not correctly advance to the last item."
  );
  buffer.advanceReadIndex(1); // Attempt to advance beyond buffer size
  console.assert(
    buffer.read() === "3",
    "Failed: Read index advanced beyond buffer content."
  );

  // Reset and test overwriting
  buffer.push("4"); // Overwrites "1"
  buffer.push("5"); // Overwrites "2"
  buffer.rewindReadIndex(3); // Move back to read "3"
  console.assert(
    buffer.read() === "3",
    "Failed: Incorrect data after overwriting and rewinding."
  );

  // Test reading from empty buffer
  const newBuffer = new CircularBufferArray(2);
  console.assert(
    newBuffer.read() === null,
    "Failed: Read from empty buffer did not return null."
  );

  // Test edge case of single-item buffer (advance and rewind should have limited effect)
  const singleItemBuffer = new CircularBufferArray(1);
  singleItemBuffer.push("single");
  console.assert(
    singleItemBuffer.read() === "single",
    "Failed: Single item buffer read incorrect."
  );
  singleItemBuffer.advanceReadIndex();
  console.assert(
    singleItemBuffer.read() === "single",
    "Failed: Advance on single item buffer changed read index."
  );
  singleItemBuffer.rewindReadIndex();
  console.assert(
    singleItemBuffer.read() === "single",
    "Failed: Rewind on single item buffer changed read index."
  );

  // Fill buffer, then completely rewind and advance
  buffer.push("6"); // Buffer now ["4", "5", "6"]
  buffer.advanceReadIndex(2); // Attempt to advance to "6"
  buffer.rewindReadIndex(2); // Rewind back to "4"
  console.assert(
    buffer.read() === "4",
    "Failed: Incorrect data after full rewind."
  );

  console.log("CircularBufferArray edge case tests completed.");
})();
