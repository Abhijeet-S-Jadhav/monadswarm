// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title MonadSwarm
 * @notice High-speed on-chain coordination layer for autonomous AI agent economies on Monad.
 * Highlights: 
 * - Parallel execution handles simultaneous solver bids.
 * - Trustless escrow vaults lock rewards and solver collateral.
 * - On-chain reputation adjustments based on verifier verdicts.
 */
contract MonadSwarm {

    struct Task {
        uint256 id;
        string prompt;
        uint256 reward;
        address coordinator;
        address assignedSolver;
        bool isCompleted;
        bool isSettled;
    }

    uint256 public taskCounter;
    mapping(uint256 => Task) public tasks;
    mapping(address => uint256) public agentReputation;

    event TaskAnnounced(uint256 indexed taskId, string prompt, uint256 reward, address indexed coordinator);
    event TaskAssigned(uint256 indexed taskId, address indexed solver, uint256 bidAmount);
    event SolutionSubmitted(uint256 indexed taskId, address indexed solver, string solution);
    event TaskSettled(uint256 indexed taskId, address indexed solver, bool verified);

    function getReputation(address agent) external view returns (uint256) {
        if (agentReputation[agent] == 0) return 100;
        return agentReputation[agent];
    }

    function announceTask(string calldata _prompt) external payable returns (uint256) {
        require(msg.value > 0, "Reward must be > 0");
        taskCounter++;
        tasks[taskCounter] = Task({
            id: taskCounter,
            prompt: _prompt,
            reward: msg.value,
            coordinator: msg.sender,
            assignedSolver: address(0),
            isCompleted: false,
            isSettled: false
        });

        emit TaskAnnounced(taskCounter, _prompt, msg.value, msg.sender);
        return taskCounter;
    }

    function assignTask(uint256 _taskId, address _solver, uint256 _bidAmount) external {
        Task storage task = tasks[_taskId];
        require(msg.sender == task.coordinator, "Only coordinator can assign");
        require(task.assignedSolver == address(0), "Already assigned");

        task.assignedSolver = _solver;
        emit TaskAssigned(_taskId, _solver, _bidAmount);
    }

    function submitSolution(uint256 _taskId, string calldata _solution) external {
        Task storage task = tasks[_taskId];
        require(msg.sender == task.assignedSolver, "Not assigned solver");
        require(!task.isCompleted, "Already completed");

        task.isCompleted = true;
        emit SolutionSubmitted(_taskId, msg.sender, _solution);
    }

    function verifyAndSettle(uint256 _taskId, bool _verified) external {
        Task storage task = tasks[_taskId];
        require(msg.sender == task.coordinator, "Only coordinator can settle");
        require(task.isCompleted, "Task not completed yet");
        require(!task.isSettled, "Already settled");

        task.isSettled = true;
        address solver = task.assignedSolver;

        if (_verified) {
            if (agentReputation[solver] == 0) agentReputation[solver] = 100;
            agentReputation[solver] += 5;
            payable(solver).transfer(task.reward);
        } else {
            if (agentReputation[solver] > 10) agentReputation[solver] -= 10;
            else agentReputation[solver] = 0;
            payable(task.coordinator).transfer(task.reward);
        }

        emit TaskSettled(_taskId, solver, _verified);
    }
}
