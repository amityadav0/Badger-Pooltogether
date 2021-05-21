// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.7.0;

interface IWBTC {
    function decimals() external view returns (uint8);

    function allowance(address owner, address spender) external returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function transferFrom(
        address from,
        address account,
        uint256 amount
    ) external returns (bool);

    function transfer(address account, uint256 amount) external returns (bool);

    function approve(address spender, uint256 amount) external returns (bool);
}